// Global variables
const getEnv = (name, fallback) => {
    const v = __ENV[name];
    // Accept empty-string as “not set” too (k6 passes env vars as strings)
    return v !== undefined && v !== '' ? v : fallback;
};

export const variables = {
    pyadcs: {
        baseUrl: getEnv('BASE_URL', 'http://localhost:8000'),
        authorityUuid: getEnv('AUTHORITY_UUID'),
        payloadPath: getEnv('PAYLOAD_PATH'),
        logging: {
            enabled: getEnv('LOGGING_ENABLED', 'false'),
        }
    },
};
