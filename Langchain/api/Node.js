const axios = require('axios');

module.exports = async function (context, req) {
    context.log('JavaScript HTTP trigger function processed a request.');

    const payload = req.body || {};

    try {
        // Replace 'LANGCHAIN_API_ENDPOINT' and 'LANGCHAIN_API_KEY' with actual values
        const langchainResponse = await axios.post(LANGCHAIN_API_ENDPOINT, payload, {
            headers: { 'Authorization': `Bearer ${LANGCHAIN_API_KEY}` }
        });

        context.res = {
            // status defaults to 200
            body: langchainResponse.data
        };
    } catch (error) {
        context.res = {
            status: 500,
            body: "Error calling Langchain API"
        };
    }
};
