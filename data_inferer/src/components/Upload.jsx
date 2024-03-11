import React, { useState } from 'react';
import axios from 'axios';
import Table from './Table'; // Import the Table component

const Upload = () => {
    const [file, setFile] = useState(null);
    const [responseData, setResponseData] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleFileUpload = async () => {
        if (!file) {
            alert('Please select a file');
            return;
        }
        setLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/api/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setResponseData(response.data);

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while uploading the file');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>File Upload</h1>
            <div>
                <input type="file" onChange={handleFileChange}/>
                <button onClick={handleFileUpload}>Upload File</button>
                {loading && <span style={{ marginLeft: '10px' }}>Loading...</span>} {/* Display "Loading..." if loading is true */}
            </div>
            {responseData &&
                <Table data={responseData} itemsPerPage={5}/>} {/* Render Table component if responseData exists */}
        </div>
    );
};

export default Upload;