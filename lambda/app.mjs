import { getBody } from './body.js';
import { index } from './index.js';

export const lambdaHandler = async (event, context) => {
    var userAgent = "unknown";
    if (event.hasOwnProperty('params') && event.params.hasOwnProperty('header') && event.params.header.hasOwnProperty('User-Agent')) {
        userAgent = event.params.header["User-Agent"];
    }
    const body = getBody(userAgent);
    return {
        statusCode: 200,
        headers: {
            "Content-Type": "text/html"
        },
        body: index(body)
    };
}