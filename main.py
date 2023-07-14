import pandas as pd
import streamlit as st
import tempfile
import os
import matplotlib.pyplot as plt
import plotly.express as px


def merge_csv_databases(bases, merge_key):
    merged_df = None

    for base in bases:
        df = pd.read_csv(base)
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on=merge_key, how='inner')

    return merged_df


# Streamlit app
def main():
    st.title("Base de données CSV")

    # Database selection
    st.header("Sélection des bases")
    numbases = st.number_input("Nombre de bases", min_value=1, max_value=5, value=1, step=1)
    databases = []
    for i in range(numbases):
        base = st.file_uploader(f"Base de données {i + 1}", type="csv")
        if base is not None:
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(base.read())
                databases.append(temp_file.name)

    # Merge key selection
    st.header("Sélection de la variable de fusion")
    merge_key_options = []
    if len(databases) > 0:
        df = pd.read_csv(databases[0])
        merge_key_options = df.columns.tolist()
    merge_key = st.selectbox("Variable de fusion", merge_key_options)

    # Merge button
    if st.button("Fusionner"):
        if len(databases) > 1:
            merged_df = merge_csv_databases(databases, merge_key)
            st.dataframe(merged_df)

            # Add boxplot
            st.subheader("Diagramme en boîte ")
            plt.figure(figsize=(8, 6))
            boxprops = dict(color='skyblue')
            medianprops = dict(color='black')
            merged_df.boxplot(column='age', by='product_id', boxprops=boxprops, medianprops=medianprops)
            plt.xlabel('ID de produit')
            plt.ylabel('Âge')
            plt.title('Diagramme en boîte : Âge par ID de produit')
            st.pyplot(plt)

            # Add pie chart
            st.subheader("Diagramme circulaire : Répartition par genre")
            gender_counts = merged_df['gender'].value_counts()
            fig = px.pie(values=gender_counts, names=gender_counts.index, title='Répartition des genres')
            st.plotly_chart(fig)

            # Add blue colored field with sum of price variable
            st.subheader("Le chiffre d'affaire")
            sum_price = merged_df['price'].sum()
            st.write(f"Total : {sum_price} €", unsafe_allow_html=True)

    # Remove the temporary files
    for base in databases:
        os.remove(base)


if __name__ == '__main__':
    main()