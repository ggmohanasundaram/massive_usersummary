# Massive User Summary
# OverView
    Massive user summary contais 3 majoy components
        1. DetailDataGenerator(app/src/data/detail_data_generator.py) - emits the raw data into kafka 
        2. SummaryDataGenerator(app/src/data/summary_data_generator.py) - consume the raw data from kafka,validate 
           it against schema and transform them into user_summary. 
           The user_Summary is pushed into an another topic when there are any changes in last seen
           and first seen values 
        3. SummaryDataReader(app/src/data/summary_data_generator.py) - consume the user_summary data from kafka


# Highlights
    1. Kafka configurations have been decoupled from code, hence the code can be run with 
       differnt kafka configuratios. 
    2. SummaryDataGenerator filters invalid/position messages from kafka and maintain them in a list.
       This can be used to analyse the issues with raw data and help source systems to fix the data quality 
       problems
    3. The problem statment doesn't explain about the aggregation window. The below assumptions was made to 
       generate the user_summary details
        1. New user - There are no records in memory
            - send a user summary with  ['Metadata']['timestamp'] as firstseen and lastseen 
        2. Existing user - 
            - if firstseen >  ['Metadata']['timestamp'] 
                update ['Metadata']['timestamp'] as firstseen and send a user summary
              else if lastseen <  ['Metadata']['timestamp'] 
                update ['Metadata']['timestamp'] as lastseen and send a user summary
                
# How To Run
    Step 1 : pip install -r requirements.txt
    Step 2 : python main.py --configname application_config.yaml --messagecount 10
             application_config.yaml(app\src\config\application_config.yaml) - contains kafka configuration
             messagecount - Number of Raw messages which DetailDataGenerator to produce
             
             
# Unit Tests
    massive_usersummary/app/test
             
             
            
    
