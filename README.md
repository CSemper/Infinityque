# Infinity Customer Tracker App 2000 :exclamation:
## 100 locations, 1 Infinity Customer Tracker ![Deploy main branch](https://github.com/data-engineering-bir-1/team-3-project/workflows/Deploy%20main%20branch/badge.svg)

### _Description_:  
<img align="right" img src="https://user-images.githubusercontent.com/70574102/96183200-77567880-0f2e-11eb-8eff-e6121a86e790.png" width="150" height="150" />

The **Infinity Customer Tracker App 2000** is a solution-based application designed for Infinty Cafe's franchise managers located all around the UK. Unlike the
previous CSV back-up system, this serverless application allows managers to:  
1. Access real data from over 100 cafe locations;  
2. Identify local and regional customer trends;  
3. Use this information to make informed and impactful decisions.

<br/> 

<img align="right" img src="https://user-images.githubusercontent.com/70574102/96180218-04e39980-0f2a-11eb-8cf0-e2afdd60ff37.png" width="150" height="150" />

### _Technologies & Architectures_:
* **Languages:** Python 3.8, Yaml<br/> 
* **SaaS:** Serverless<br/> 
* **Cloud Provider:** AWS<br/> 
   * **Storage:** Amazon S3
   * **Compute:** AWS Lambda 
   * **Integration** Amazon SQS
   * **Analytics:** Amazon Redshift, Amazon Quicksight

<br/> 
 

### _How it Works_:
<img align="right" img src="https://user-images.githubusercontent.com/70574102/96183787-56daee00-0f2f-11eb-8f30-92c924771976.png" width="150" height="150" />

A CloudWatch Event rule is used to automate the configured ETL process, so that the entire function is triggered daily.<br />
The ETL process **(Extract, Transform, Load)** allows data to be gathered from multiple sources and consolidated it into a
single, centralized location. Python Package *boto3* is used to extract raw CSV data from an S3 bucket.<br />
The raw data is then transformed and cleaned, using Amazon Simple Queue Service (SQS) to integrate three separate Lamdas.<br />
The Python Package *psycopg2* is used to load this transformed data to a relational Redshift Database.<br />

>> Entire process starts at (time) daily, finishes at (time), taking a total of (time). Costs (£)

[Example Code Here]

<br/> 


### _Tests_:
<img align="right" img src="https://user-images.githubusercontent.com/70574102/96183671-1da27e00-0f2f-11eb-8ae0-921d8553e5f3.png" width="150" height="150" />

(To be updated with info on what tests are included and sample code)




### _Contributors_:
**Team 3**, Data Engineering Cohort, Birmingham Edition :mortar_board:
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://www.linkedin.com/in/jacob-callear/"><img src="https://user-images.githubusercontent.com/70574102/96184723-c69da880-0f30-11eb-9d19-020937e8e7ef.png" width="100px;" alt=""/><br /><sub><b>Jacob Callear</b></sub></a><br /><a href="https://github.com/jacobcallear" title="Documentation">📖</a> <sub><b>:bird:</b></sub></a></td>
    <td align="center"><a href="https://www.linkedin.com/in/shameela-b/"><img src="https://user-images.githubusercontent.com/70574102/96185848-7293c380-0f32-11eb-9567-10c1b46f7d9c.png" width="100px;" alt=""/><br /><sub><b>Shameela Begum</b></sub></a><br /><a href="https://github.com/Shameela8" title="Documentation">📖</a> <sub><b>:gem:</b></sub></a></td>
     <td align="center"><a href="https://www.linkedin.com/in/hamza-bash/"><img src="https://user-images.githubusercontent.com/70574102/96186183-fc439100-0f32-11eb-8d10-9ed9e95c22e4.png" width="100px;" alt=""/><br /><sub><b>Hamza Bashir</b></sub></a><br /><a href="https://github.com/hamzabash" title="Documentation">📖</a> <sub><b>:chart_with_upwards_trend:</b></sub></a></td>
     <td align="center"><a href="https://www.linkedin.com/in/chenyse-semper"><img src="https://user-images.githubusercontent.com/70574102/96186640-a7544a80-0f33-11eb-9cd6-989470846ffb.png" width="100px;" alt=""/><br /><sub><b>Chenyse Semper</b></sub></a><br /><a href="https://github.com/CSemper" title="Documentation">📖</a> <sub><b>:sunflower:</b></sub></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://www.linkedin.com/in/andrei-ilici/"><img src="https://user-images.githubusercontent.com/70574102/96186903-04e89700-0f34-11eb-8cc9-61d09315225d.png" width="100px;" alt=""/><br /><sub><b>Andrei Ilicir</b></sub></a><br /><a href="https://github.com/Andrei-Ilici" title="Documentation">📖</a> <sub><b>:bulb:</b></sub></a></td>
    <td align="center"><a href="https://www.linkedin.com/in/jaspreet-singh-bains-25824a193/"><img src="https://user-images.githubusercontent.com/70574102/96187103-5729b800-0f34-11eb-8b1b-02f3012ac2e8.png" width="100px;" alt=""/><br /><sub><b>Jaspreet "Jazz" Singh</b></sub></a><br /><a href="https://github.com/Jaspreet1188" title="Documentation">📖</a> <sub><b>:email:</b></sub></a></td>
     <td align="center"><a href="https://www.linkedin.com/in/jawad-khan-0354681a1/"><img src="https://user-images.githubusercontent.com/70574102/96187434-e8009380-0f34-11eb-9670-7740dfbff975.png" width="100px;" alt=""/><br /><sub><b>Jawad Khan</b></sub></a><br /><a href="https://github.com/jawad46" title="Documentation">📖</a> <sub><b>:mag:</b></sub></a></td>
     <td align="center"><a href="http://lewis.com"><img src="https://user-images.githubusercontent.com/70574102/96187827-93114d00-0f35-11eb-9a64-a3e5722015f7.png" width="100px;" alt=""/><br /><sub><b>Lewis Richardson</b></sub></a><br /><a href="https://github.com/lewisrichardson" title="Documentation">📖</a> <sub><b>:smiley_cat:</b></sub></a></td>
