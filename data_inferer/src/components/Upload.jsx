import React, {useEffect, useState} from 'react';
import axios from 'axios';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [responseData, setResponseData] = useState(null);

    useEffect(() => {
        if (responseData) {
            console.log(Object.keys(responseData['df']));
            alert(responseData.message);
        }
    }, [responseData]); // This effect runs when responseData changes

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleFileUpload = async () => {
        if (!file) {
            alert('Please select a file');
            return;
        }

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
        }
    };

    const renderTable = (data) => {
        console.log(data);
        if (!data || !data['df']) return null;
        return (
            <table>
                <thead>
                    <tr>
                        {Object.keys(data['df']).map((key) => (
                            <th key={key}>{key}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data['df'][Object.keys(data['df'])[0]].map((_, rowIndex) => (
                        <tr key={rowIndex}>
                            {Object.keys(data['df']).map((columnName, colIndex) => (
                                <td key={`${rowIndex}-${colIndex}`}>{data['df'][columnName][rowIndex]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    return (
        <div>
            <h1>File Upload</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Upload File</button>
            {responseData && renderTable(responseData)}
        </div>
    );
};

export default Upload;
