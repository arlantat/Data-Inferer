import React, { useState } from 'react';
import axios from 'axios';
import Table from './Table'; // Import the Table component

const Upload = () => {
    const [file, setFile] = useState(null);
    const [responseData, setResponseData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [loadingTime, setLoadingTime] = useState('0');

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleFileUpload = async () => {
        if (!file) {
            alert('Please select a file');
            return;
        }
        setLoading(true);
        const start = new Date();

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/api/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setResponseData(response.data);
            console.log(response.data);
        } catch (error) {
            if (error.response) {
                console.error('Error response:', error.response.data);
                alert(error.response.data.error);
            } else {
                console.error('Error:', error);
                alert('An error occurred while uploading the file');
            }
        } finally {
            setLoading(false);
            const end = new Date();
            setLoadingTime(((end - start) / 1000).toFixed(3));
        }
    };

    return (
        <div>
            <h1 className="m-3">Data Inferer</h1>
            <div className="m-3">
                <input type="file" className="form-control-file" onChange={handleFileChange}/>
                <button className="btn btn-secondary" style={{ backgroundColor: "#00748f" }} onClick={handleFileUpload}>Upload File</button>
                <span className="m-5">Time elapsed: {loadingTime}s</span>
                {loading && <span className="ml-2">Loading...</span>}
            </div>
            {responseData && <Table data={responseData} itemsPerPage={5}/>}
        </div>
    );
};

export default Upload;