const axios = require('axios');
const { BlobServiceClient } = require('@azure/storage-blob');
const XLSX = require('xlsx');

// You might need to adjust this import based on the actual Langchain SDK or API you're using
// const LangChain = require('langchain'); 

module.exports = async function (context, req) {
    // Determine if the request is for file processing or a text prompt
    if (req.body && req.body.prompt) {
        // Handle text prompt
        try {
            const langchainResponse = await axios.post('Your Langchain API Endpoint', { prompt: req.body.prompt }, {
                headers: { 'Authorization': `Bearer Your Langchain API Key` }
            });

            context.res = {
                body: langchainResponse.data
            };
        } catch (error) {
            context.res = {
                status: 500,
                body: "Error calling Langchain API: " + error.message
            };
        }
    } else if (req.body && req.body.file) {
        // Handle file upload
        try {
            const blobServiceClient = BlobServiceClient.fromConnectionString(process.env.AzureWebJobsStorage);
            const containerClient = blobServiceClient.getContainerClient('file-uploads');
            await containerClient.createIfNotExists();

            const blobName = 'uploaded-file-' + new Date().getTime(); // Ensure unique name
            const blockBlobClient = containerClient.getBlockBlobClient(blobName);

            await blockBlobClient.uploadData(req.body.file);

            // Assuming file content needs to be read as text
            const downloadBlockBlobResponse = await blockBlobClient.download(0);
            const fileContent = await streamToString(downloadBlockBlobResponse.readableStreamBody);

            // Here, implement logic based on file type, e.g., CSV or XLSX parsing
            // For demonstration, this part is left as a placeholder
            
            // Assume function to process data and get insights
            const insights = await getInsightsFromData(fileContent); // This should be implemented based on your logic

            context.res = {
                body: { insights }
            };
        } catch (error) {
            context.res = {
                status: 500,
                body: "Error processing file: " + error.message
            };
        }
    } else {
        // Handle incorrect request type
        context.res = {
            status: 400,
            body: "Invalid request"
        };
    }
};

async function streamToString(stream) {
    const chunks = [];
    return new Promise((resolve, reject) => {
        stream.on('data', (chunk) => chunks.push(chunk));
        stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')));
        stream.on('error', reject);
    });
}

async function getInsightsFromData(data) {
    // Placeholder for processing data and getting insights
    // This could involve parsing CSV/XLSX data, calling Langchain with processed data, etc.
    // Return insights as a string or structured object
    return "Insights based on uploaded data"; // Placeholder response
}
