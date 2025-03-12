import json
from dotenv import load_dotenv
from src.generator import GeneratorAgent

load_dotenv()

def lambda_handler(event, context):
    body = event['body']\

    retrieved_data = body.get('retrievedData')
    query = body.get('query')
    msg_history = body.get('msgHistory')
    session_id = body.get('sessionId')

    context = "\n".join(
        [item['content']['text'] for item in retrieved_data]
    )

    agent = GeneratorAgent()
    reply: str = agent.generate_response(query, context)

    msg_history.extend([
        {'role': 'user', 'content': query},
        {'role': 'system', 'content': reply}
    ])

    payload = {
        "response": reply,
        "msgHistory": msg_history,
        "sessionId": session_id
    }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(payload)
    }

event = {
    "body": {
        "retrievedData": [
            {
                "content": {
                    "text": "The imperative categories are: university mission, leaders and cultures, teaching and learning, digital solutions, knowledge generation and discovery, and revenue diversification. Each imperative requires key policy considerations to be fully and sustainably actualized.19     Six university design imperatives and key policy questions     Focused on continuity and sustainable change, the higher education sector should demonstrate flexible and agile leadership and investments in leadership at multiple levels. It is also critical to develop explicit design expertise in current and future leaders to accelerate and scale impact.     Policy Considerations     • How can policy inform universities and higher education regulatory bodies in making staffing decisions?     • How can policy empower expertise while encouraging new ideas and experience in higher education leadership?     • What are the current trends in rules governing hiring practices in higher education?     Rewriting the very reason for being, the university mission is now charged with expanding beyond academics and research to incorporate broader societal concerns and needs - needs to include access, diversity of learners, and lifelong learning.     Policy Considerations     • Who has the authority to mandate the mission? The university vs. the regulatory bodies?     • How can policies be shaped to motivate innovation in higher education to overcome long standing hardships?     • How can policy operationalize the social, economic, and political roles of higher education institutions in national and international communities?",
                    "type": "TEXT"
                },
                "location": {
                    "s3Location": {
                        "uri": "s3: //udi-docs/doc-b.pdf"
                    },
                    "type": "S3"
                },
                "metadata": {
                    "x-amz-bedrock-kb-source-uri": "s3: //udi-docs/doc-b.pdf",
                    "x-amz-bedrock-kb-document-page-number": 18.0,
                    "x-amz-bedrock-kb-data-source-id": "URCTFQITVD"
                },
                "score": 0.5118964910507202
            },
            {
                "content": {
                    "text": "Michael Crow has been president of Arizona State University (ASU) for over 20 years ushering transformative change in the mission, vision, and values of the institution through a design-thinking model. U.S. News and World Report has ranked ASU the most innovative university in the U.S. for 8 consecutive years. President Crow is chair of the University Design Institute (UDI). A detailed review of ASU’s design journey is included in the book, Redesigning Higher Education, available here: https: //udi.asu.edu/redesigning-higher-education     18     “     Through co-design work with over 100 institutions in nearly two-dozen countries, the University Design Institute (UDI) has identified six core design imperatives that create the culture and structure of how a sustainably redesigned university functions. Though labeled differently across organizations and in the literature, the six non-mutually exclusive imperatives are in harmony with major trends currently identified as attention-critical around the world. And underlying success in each of these imperatives is a dependence on diverse and efficient university financial models. The imperative categories are: university mission, leaders and cultures, teaching and learning, digital solutions, knowledge generation and discovery, and revenue diversification.",
                    "type": "TEXT"
                },
                "location": {
                    "s3Location": {
                        "uri": "s3://udi-docs/doc-b.pdf"
                    },
                    "type": "S3"
                },
                "metadata": {
                    "x-amz-bedrock-kb-source-uri": "s3://udi-docs/doc-b.pdf",
                    "x-amz-bedrock-kb-document-page-number": 18.0,
                    "x-amz-bedrock-kb-data-source-id": "URCTFQITVD"
                },
                "score": 0.39322102069854736
            },
            {
                "content": {
                    "text": "Since 2019, UDI has engaged more than 50% of colleges at ASU and supported innovation and co-design efforts in over 100 institutions in close to two dozen countries.     University Design Institute17 World Government Summit     Financial sustainability has been the single biggest existential threat facing the higher education (HE) sector today.”1     Executive Summary     6     Around the globe, higher education has tended to rely heavily on one or two sources for financing - government revenue and tuition. There have been many indicators and proof points of the vulnerability of this model over the past several decades; however, a unique combination of the hastening fourth industrial revolution and the COVID-19 pandemic exacerbated the risks and forced action.2 For some institutions, the results ranged from program cuts to tuition hikes to mergers and ultimately closure. For those institutions that actually remained solvent and maintained their prior offerings and ownership models, sustainable revenue diversification continues to emerge as a fundamental, yet somewhat elusive, design goal.     While true transformative change challenges most businesses, the “business” of higher education involves a few unique layers that further complicate the whats, whys, and hows of systemic overhauls. Higher education is not the most flexible industry. Rather, the     “7     1 Jisc & Emerge Education. (2021, Mar). The future of revenue diversification in higher education. From fixes to foresight: Jisc and Emerge Education insights for universities and startups.",
                    "type": "TEXT"
                },
                "location": {
                    "s3Location": {
                        "uri": "s3: //udi-docs/doc-b.pdf"
                    },
                    "type": "S3"
                },
                "metadata": {
                    "x-amz-bedrock-kb-source-uri": "s3://udi-docs/doc-b.pdf",
                    "x-amz-bedrock-kb-document-page-number": 5.0,
                    "x-amz-bedrock-kb-data-source-id": "URCTFQITVD"
                },
                "score": 0.33122947812080383
            }
        ],
        "query": "What are the UDI design imperatives?",
        "msgHistory": [],
        "sessionId": 1
    }
}

lambda_handler(event, None)