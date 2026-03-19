# Methodology: End-to-End EDM Process Analytics

This document details the mathematical heuristics, machine learning algorithms, and probabilistic models used to automatically map data lineage and uncover operational contexts within the Enterprise Data Management (EDM) system.

---

## Phase 1: Heuristic Discovery of Schema & Relationships

Traditional EDM analysis relies on static data dictionaries. This pipeline programmatically discovers temporal anchors and primary keys across disconnected tables using statistical heuristics.

### 1.1 Temporal Anchor Identification
To track data flow, we must first identify reliable timestamp columns (e.g., insertion or update times) without relying on column names.
*   **Variance and Dispersion:** We calculate the standard deviation ($\sigma$) and Interquartile Range (IQR) of all datetime columns. Columns with near-zero variance are discarded as static metadata (e.g., system epoch dates).
*   **Shannon Entropy:** To ensure the timestamp column represents continuous transactional flow rather than batch-inserted dummy dates, we calculate Shannon Entropy for the temporal distribution:
    $$H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$
    Columns exceeding a predefined entropy threshold are classified as active temporal anchors.

### 1.2 Primary Key (PK) Mapping via Divergence
To trace an entity across tables, we must identify which columns act as shared identifiers (Primary Keys).
*   **Distribution Matching:** We compute the frequency distribution of categorical/alphanumeric values in candidate columns.
*   **Jensen-Shannon (JS) Divergence:** To map relationships between Table A and Table B, we measure the similarity between candidate column distributions $P$ and $Q$. We use JS Divergence because it is symmetric and smoothed:
    $$JSD(P \parallel Q) = \frac{1}{2} D_{KL}(P \parallel M) + \frac{1}{2} D_{KL}(Q \parallel M)$$
    *(where $M = \frac{1}{2}(P + Q)$ and $D_{KL}$ is the Kullback-Leibler divergence).*
    Pairs with a $JSD$ approaching $0$ are flagged as relational links (e.g., `TableA.CADIS_ID` $\rightarrow$ `TableB.CADIS_ID`).

---

## Phase 2: Unsupervised Traversal Clustering

Once keys and timestamps are identified, we build a "table presence matrix" (a boolean matrix where rows are unique PKs and columns are EDM tables). 

### 2.1 Dimensionality Reduction (MCA)
Because the table presence matrix is sparse, high-dimensional, and binary, standard PCA is ineffective. We apply **Multiple Correspondence Analysis (MCA)** to reduce dimensionality while preserving the variance of categorical traversal paths. 

### 2.2 Traversal Behavior Clustering
We apply **K-Means Clustering** on the MCA-reduced feature space to group primary keys that take similar paths through the EDM.
*   **Optimization:** The optimal number of clusters ($k$) is determined by maximizing the Silhouette Score, ensuring tight, distinct groupings of processing behaviors (e.g., Cluster 0 = standard equities flow, Cluster 1 = options exception flow).
    $$s(i) = \frac{b(i) - a(i)}{\max\{a(i), b(i)\}}$$
    *(where $a(i)$ is the mean intra-cluster distance and $b(i)$ is the mean nearest-cluster distance).*

---

## Phase 3: Supervised Context Extraction

Knowing *how* data moves (clusters) is only half the battle; we must know *why* it moves that way. We extract raw transactional features (e.g., `ASSET_CLASS`, `CURRENCY`, `BROKER_ID`) and use them to predict the K-Means clusters.

### 3.1 Random Forest Feature Importance
We train a **Random Forest Classifier** where:
*   **Features ($X$):** The raw, domain-specific columns extracted from the primary EDM tables.
*   **Target ($y$):** The cluster ID assigned in Phase 2.

We extract the **Mean Decrease in Impurity (Gini Importance)** from the trained model to rank which specific data contexts drive the traversal paths:
$$I_G(t) = 1 - \sum_{i=1}^{c} p(i|t)^2$$
*(where $p(i|t)$ is the fraction of records belonging to class $i$ at node $t$).* 
High-importance features definitively explain the operational logic behind different routing paths.

---

## Phase 4: Probabilistic Process Mapping & Latency

### 4.1 Markov Chain Sequencing
Using the temporal anchors from Phase 1, we chronologically sort the table traversals for every primary key. We model this sequence as a discrete-time Markov Chain to build a probabilistic map of the system.
*   **Transition Probability Matrix:** We calculate the probability of moving from Table $i$ to Table $j$:
    $$P_{i,j} = P(X_{n+1} = j \mid X_n = i) = \frac{N_{i,j}}{\sum_{k} N_{i,k}}$$
    *(where $N_{i,j}$ is the observed count of transitions from $i$ to $j$).*

### 4.2 Straight Through Processing (STP) Latency Analysis
Finally, we calculate the time delta ($\Delta t$) between $X_n$ and $X_{n+1}$.
*   **STP Classification:** Transitions that occur within the expected temporal baseline (e.g., $\Delta t < 5 \text{ seconds}$) are classified as STP.
*   **Bottleneck Detection:** Transitions exceeding the 95th percentile of $\Delta t$ for a given $P_{i,j}$ path are flagged as non-STP anomalies, highlighting exact tables where processing stalls or manual intervention occurs.
