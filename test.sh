curl --request GET \
--url 'http://127.0.0.1:3000/vectorise/?=' \
--header 'Content-Type: application/json' \
--data '{
"language": "en",
"vectorise": ["Identify relevant market framework conditions of carmakers\n Realize the economic importance of the automotive industry\n Know automotive key figures in respect to particular countries\n Categorize the product portfolio of automotive suppliers\n Examine and understand future trends of automotive markets and resource requirements of carmakers"]}'

curl --request GET \
--url 'http://127.0.0.1:3000/course_by_instructor/?=' \
--header 'Content-Type: application/json' \
--data '{"instructor": "Chantelau"}'

curl --request GET \
--url 'http://127.0.0.1:3000/course_by_title/?=' \
--header 'Content-Type: application/json' \
--data '{"intitle": "software"}'
