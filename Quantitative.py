import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import streamlit_shadcn_ui as ui

def quantitative_analysis():


  #import excel file name disabilitycensus2021.xlsx sheet name Table 6

  df = pd.read_excel('Data/disabilitycensus2021.xlsx', sheet_name='Table 6')

  st.title('Quantitative Analysis')


  tab1, tab2, tab3, tab4 = st.tabs(['Census 2021', 'SEN Dashboard', 'Employment', 'Education'])
  with tab1:
    st.header('Census 2021')
    # Create two columns for the multiselects
    col1, col2 = st.columns(2)

    # Place each multiselect in one column
    with col1:
      local_authority = st.multiselect('Local Authority', df['Local Authority'].unique(), default=['Brent'])
    with col2:
      age_group = st.multiselect('Age Group', df['Age'].unique(), default=['15 to 19'])


    #write code if nothing is selected for local_authority and age_group then display a message to select local_authority and age_group for the data to be displayed
    if len(local_authority) == 0 or len(age_group) == 0:
        st.write('Please select Local Authority and Age Group')
    else:

      #display the selected local authority and age group
      #st.write('Selected Local Authority:', local_authority)
      #st.write('Selected Age Group:', age_group)


      st.header('Borough Level Disabled Population Analysis')

      #filter the data based on the selected local authority and age group
      disabled_population = df[(df['Local Authority'].isin(local_authority))
                          & (df['Age'].isin(age_group))
                          & (df['Category'] == 'Four category')
                          & (df['Sex'].isin(['Male','Female']))
                          & (df['Disability Status'].isin(['Disabled; limited a lot','Disabled; limited a little']))]

      st.write('Disabled Population:', disabled_population['Count'].sum())

      # Total population

      total_population = df[(df['Local Authority'].isin(local_authority))
                          & (df['Age'].isin(age_group))
                          & (df['Category'] == 'Four category')
                          & (df['Sex'].isin(['Male','Female']))
                          & (df['Disability Status'].isin(['Disabled; limited a lot']))]

      st.write('Total Population:', total_population['Population'].sum())

      total_UK_population = df[(df['Local Authority'].isin(df['Local Authority'].unique()))
                          & (df['Age'].isin(df['Age'].unique()))
                          & (df['Category'] == 'Four category')
                          & (df['Sex'].isin(['Male','Female']))
                          & (df['Disability Status'].isin(['Disabled; limited a lot']))]
      
      st.write('Total UK Population:', total_UK_population[total_UK_population['Population'] != '[c]']['Population'].sum())

      percentage_uk_population = (total_population['Population'].sum() / total_UK_population[total_UK_population['Population'] != '[c]']['Population'].sum()) * 100
      
      st.markdown("""
      <style>
          .stCard>div {
              height: 150px;  /* Adjust the height as needed */
          }
      </style>
      """, unsafe_allow_html=True)
      
      #Total Population and Disabled Population in a card
      cols = st.columns(3)
      with cols[0]:
        total_uk_population_millions = round(total_UK_population[total_UK_population['Population'] != '[c]']['Population'].sum() / 1e6, 2)
        ui.metric_card(title="UK Poulation", content= total_uk_population_millions, description='In Millions', key="card0")
      with cols[1]:
        content = f"{total_population['Population'].sum():,} ({percentage_uk_population:.2f}%)"
        ui.metric_card(title="Total Population", content=content, description="Percentage of UK population ", key="card1")
      with cols[2]:
        # Calculate the percentage of disabled population out of total population
        percentage_disabled = (disabled_population['Count'].sum() / total_population['Population'].sum()) * 100

        # Format the content to include both the sum and the percentage
        content = f"{disabled_population['Count'].sum():,} ({percentage_disabled:.2f}%)"

        # Update the ui.metric_card to display the new content
        ui.metric_card(title="Disabled Population", content=content, description="Percentage of Borough population", key="card2")
      

          # Add space between card and plots
      st.markdown(" " * 5)  # Adjust the number of "\n" based on the desired space
      
      # Create a figure for 4x1 subplots
      fig, axs = plt.subplots(3, 1, figsize=(12, 35)) 

      # Plot 1: Total Population vs Disabled Population
      sns.barplot(x=['Total Population', 'Disabled Population'], y=[total_population['Population'].sum(), disabled_population['Count'].sum()], ax=axs[0])
      axs[0].set_title('Total Population vs Disabled Population', fontsize=20, fontweight='bold', y=1.05)

      # Set x-axis and y-axis label with increased font size
      axs[0].set_xlabel('Category', fontsize=20)  # Increase x-axis label font size
      axs[0].set_ylabel('Population', fontsize=20)  # Increase y-axis label font size
      # Increase tick size
      axs[0].tick_params(axis='both', labelsize=18)  # Increase tick size for both axes
      # Add data labels for Plot 1 with increased font size
      for bar in axs[0].patches:
        axs[0].text(x=bar.get_x() + bar.get_width() / 2, 
              y=bar.get_height(), 
              s=f'{int(bar.get_height())}', 
              ha='center', 
              va='bottom', fontsize=18)  # Increased data label font size

      # Plot 2: Disabled Population by Sex
      st.markdown(" " * 5)  # Adjust the number of "\n" based on the desired space
      disabled_population.groupby('Sex')['Count'].sum().plot.pie(autopct='%1.1f%%', ax=axs[1], textprops={'fontsize': 18})
      axs[1].tick_params(labelsize=18)
      axs[1].set_title('Disabled Population by Sex', fontsize=20, fontweight='bold', y=1.05)

      # Plot 3: Population Group by Disability Status
      poulation_grpby_category = df[(df['Local Authority'].isin(local_authority))
                          & (df['Age'].isin(age_group))
                          & (df['Category'] == 'Four category')
                          & (df['Sex'].isin(['Male','Female']))
                          ]
      data = poulation_grpby_category.groupby('Disability Status')['Count'].sum().reset_index()
      sns.barplot(x='Disability Status', y='Count', data=data, palette='viridis', ax=axs[2])

      # Add data labels for Plot 3
      for bar in axs[2].patches:
          axs[2].text(x=bar.get_x() + bar.get_width() / 2, 
                      y=bar.get_height(), 
                      s=f'{int(bar.get_height())}', 
                      ha='center', 
                      va='bottom', fontsize=18)

      axs[2].set_ylim(0, data['Count'].max() * 1.1)
      axs[2].tick_params(axis='x', rotation=30, labelsize=18)
      axs[2].tick_params(axis='y', labelsize=18)
      axs[2].set_xlabel('Disability Status', fontsize=20)  # Increase x label font size
      axs[2].set_ylabel('Count', fontsize=20)  # Increase y label font size
      import textwrap

      # Wrap x-axis tick labels for Plot 3
      wrapped_labels = [textwrap.fill(label.get_text(), width=20) for label in axs[2].get_xticklabels()]
      axs[2].set_xticklabels(wrapped_labels, rotation=30, ha="right", fontsize=18)
      axs[2].set_title('Population Group by Disability Status', fontsize=20, fontweight='bold', y=1.05)

      # Adjust layout for the single column
      plt.tight_layout()
      # Adjust the spacing between rows of plots
      plt.subplots_adjust(hspace=0.3)  # Increase hspace as needed
      # Display the figure in Streamlit
      st.pyplot(fig)

      #display disabled population of Top 10 local authorities in a bar chart

      # Convert 'Count' column to numeric
      df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
      uk_disabled_population = df[(df['Age'].isin(age_group))
                          & (df['Category'] == 'Four category')
                          & (df['Sex'].isin(['Male','Female']))
                          & (df['Disability Status'].isin(['Disabled; limited a lot','Disabled; limited a little']))]

      # Get the top 10 local authorities by disabled population
      disabled_population_top10 = uk_disabled_population.groupby('Local Authority')['Count'].sum().nlargest(10)

      plt.figure(figsize=(10, 5))
      sns.barplot(x=disabled_population_top10.index, y=disabled_population_top10.values)
      plt.xticks(rotation=45)
      plt.title('Disabled Population For Top 10 Local Authority', fontsize=20, fontweight='bold', y=1.05) 
      st.pyplot(plt)

      #UK Map
      import uk_map

  with tab2:
    st.header('SEN Dashboard')
    st.write('Coming Soon')

  with tab3:
    st.header('Employment')
    st.write('Coming Soon')

  with tab4:
    st.header('Education')
    st.write('Coming Soon')

if __name__ == '__main__':
  quantitative_analysis()