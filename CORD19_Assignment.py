# CORD-19 Research Papers Analysis

This notebook explores the **CORD-19 metadata.csv** dataset with simple beginner-friendly analysis and visualizations.

We will:
1. Load and explore the data
2. Clean and prepare it
3. Analyze and visualize patterns
4. Build a Streamlit app separately (code provided)

# Install required packages if needed (uncomment when running first time)
# !pip install pandas matplotlib seaborn wordcloud

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

## Part 1: Data Loading & Exploration
# Load dataset
df = pd.read_csv("metadata.csv")

# First 5 rows
df.head()
# Dataset shape
print("Shape:", df.shape)

# Info
print(df.info())

# Missing values
df.isnull().sum().head(20)

## Part 2: Data Cleaning & Preparation
# Convert publish_time to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Extract year
df['year'] = df['publish_time'].dt.year

# Abstract word count
df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(x.split()))

# Drop rows without title or publish_time
df_clean = df.dropna(subset=['title', 'publish_time'])
df_clean.shape

## Part 3: Analysis & Visualizations

# Publications by Year
year_counts = df_clean['year'].value_counts().sort_index()
plt.bar(year_counts.index, year_counts.values)
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.show()

# Top Journals
top_journals = df_clean['journal'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=top_journals.values, y=top_journals.index)
plt.title("Top 10 Journals")
plt.xlabel("Number of Papers")
plt.show()

# Word Cloud of Titles
titles = " ".join(df_clean['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles)

plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Paper Titles")
plt.show()

# Papers by Source
top_sources = df_clean['source_x'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=top_sources.values, y=top_sources.index)
plt.title("Top Sources")
plt.xlabel("Number of Papers")
plt.show()

## Part 4: Streamlit App

Save the following code as **app.py** and run with:
```bash
streamlit run app.py
---

### Markdown Cell
```markdown
```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

df = pd.read_csv("metadata.csv")
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")

year_range = st.slider("Select year range:", 2015, 2025, (2019, 2021))
filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
st.pyplot(fig)

st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax)
st.pyplot(fig)

st.subheader("Word Cloud of Titles")
titles = " ".join(filtered['title'].dropna().tolist())
if titles.strip():
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.write("No titles available for selected years.")

st.subheader("Sample Data")
st.write(filtered[['title', 'authors', 'journal', 'year']].head(10))

---

### Markdown Cell
```markdown
## Part 5: Reflection

- **Findings**: Most papers are from 2020, with top journals including *medRxiv*, *The Lancet*, etc.  
- **Challenges**: Handling missing values and large dataset size.  
- **Learning**: Learned pandas basics, visualization with matplotlib/seaborn, and how to make a Streamlit app.

