# Setup

- Install node libraries. Execute the following command within `javascript_module` directory

`npm install`
 
- Run tests on Chrome, Firefox & IE using the following command

`npm run test`

- There are two distributable files, superglu-core.js contains only SuperGLU but superglu-standard.js contains additional services 
namely Heartbeat_Service, StandardITSLoggingService, LearningTask and SerializableAssistmentsItem
    - Both the files superglu-core.js and superglu-standard.js are created within dist directory using the following commands respectively
 
`npm run build-core`

`npm run build-standard`