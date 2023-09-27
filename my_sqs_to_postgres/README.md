Running Process:
Step 1: Create the user_logins table in postgres
Step 2: run "docker-compose up -d" in the terminal
Step 3: run "python app.py" in the terminal
Step 4: run "docker-compose down" in the terminal

Thought Process:
- First I needed to get the JSON data from an SQS queue, for that I used the boto3 library.
- The client function was not working as I expected and giving me a lot of errors. With some research I found out that for the client function to work I needed aws credentials.
- But then the instructions file said I didn't need an aws account to do this. So, after some more research I found out that I could use dummy access keys and that's what I did to make the client function work.

- Then I started a connection to my local database. Also I created the table manually in my postgres.

- I then retrieved the message from the image and then masked the ip and the device id and sent that data to my database.


Questions:
1. How would you deploy this application in production?
A. In production, I would deploy the application using a container orchestration tool like Kubernetes or AWS ECS. I would also configure environment-specific settings such as AWS credentials and database connection details using environment variables.

2. What other components would you want to add to make this production ready?
A. To make it production ready the other components I would add are:
- Authentication
- Error Handling
- Scalability
- Backup and Recovery

3. How can this application scale with a growing dataset?
A. Need to use the AWS SQS to decouple message processing from data ingestion.

4. How can PII be recovered later on?
A. Need to map the masked values to the original values. This way the masked values can be recovered later on.

5. What are the assumptions you made?
A. Assumption made:
- SQS queue will always contain JSON data.
- The masking algorithm is reversable.
- Performance and scalability not considered