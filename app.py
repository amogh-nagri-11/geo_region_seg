import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from krushkal import krushkal, build_graph_from_mst, find_cost_between_hubs

def load_data(uploaded_file=None):
    if uploaded_file:
        return pd.read_csv(uploaded_file)
    else:
        try:
            return pd.read_csv('locations.csv')
        except FileNotFoundError:
            st.error("Default locations.csv not found.")
            return pd.DataFrame()

def display_mst(df, mst, show_list=True):
    if show_list:
        st.subheader("Minimum Spanning Tree")
        for u, v, w in mst:
            st.write(f"{df.loc[u, 'location']} ⟷ {df.loc[v, 'location']} (Distance: {w:.2f})")

def plot_graph(df, mst, node_size, edge_color):
    st.subheader("Visual Representation")
    fig, ax = plt.subplots()
    ax.scatter(df['x'], df['y'], s=node_size, color='blue')

    for i, row in df.iterrows():
        ax.annotate(row['location'], (row['x'], row['y']), textcoords="offset points", xytext=(0, 10), ha='center')

    for u, v, _ in mst:
        x_vals = [df.loc[u, 'x'], df.loc[v, 'x']]
        y_vals = [df.loc[u, 'y'], df.loc[v, 'y']]
        ax.plot(x_vals, y_vals, color=edge_color)

    st.pyplot(fig)

def main():
    st.title("Geographic Region Segmentation for Logistic Services")

    st.markdown("""
        This app visualizes how **Kruskal's algorithm** is used to segment a geographic region for logistic services.

        Each node on the graph represents a **location**, and edges represent **the shortest connections** (based on Euclidean distance) needed to **connect all locations** with **minimum total distance**.

        This technique can help:
        - Optimize placement of Logistic service routes
        - Reduce redundancy in connections
        - Visualize minimal infrastructure needed between stations

        The red lines (or chosen color) show the **Minimum Spanning Tree (MST)** connecting all locations.
        """)

    st.sidebar.header("Configuration")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    node_size = st.sidebar.slider("Node Size", 50, 300, 100)
    edge_color = st.sidebar.color_picker("Edge Color", "#FF0000")
    show_mst_list = st.sidebar.checkbox("Show MST Edge List", value=True)

    df = load_data(uploaded_file)

    if df.empty:
        st.warning("No data to display.")
        return

    st.subheader("Input Locations")
    st.dataframe(df)

    mst = krushkal(df)
    display_mst(df, mst, show_list=show_mst_list)
    plot_graph(df, mst, node_size, edge_color)

    st.subheader("Minimum Cost Between Two Hubs")

    location_names = df['location'].tolist()
    loc_to_index = {loc: idx for idx, loc in enumerate(location_names)}

    col1, col2 = st.columns(2)
    with col1:
        hub1 = st.selectbox("Select Starting Hub", location_names)
    with col2:
        hub2 = st.selectbox("Select Destination Hub", location_names, index=1 if len(location_names) > 1 else 0)

    if hub1 != hub2:
        graph = build_graph_from_mst(mst, len(df))
        cost = find_cost_between_hubs(graph, loc_to_index[hub1], loc_to_index[hub2])
        if cost is not None:
            st.success(f"Minimum cost between **{hub1}** and **{hub2}** is **{cost:.2f}** units.")
        else:
            st.error("These hubs are not connected.")
    else:
        st.info("Please select two different hubs.")

if __name__ == "__main__":
    main()
    