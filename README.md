# SubjectCollectorInHust (Project3)

## Result
- Crawl all data of 6963 subjects in sis.hust.edu.vn
- Visualize the relationship of subjects
- (More functions in progress)

## Installation

- Clone repository
- Run the following command to import the required libraries:
`pip install -r requirements.txt`
- If you want to collect data of all subjects, run: 
`scrapy crawl course -O result.csv`
- If you want to collect information of a subject, run (with course_code is the subject code you want to collect):
`scrapy crawl course -a code=course_code -O result_search.csv`
- To render the relation file of all subjects, run file relationship and result save at folder output
