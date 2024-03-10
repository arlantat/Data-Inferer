import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Table = () => {
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(10); // Number of rows per page
    const [totalRows, setTotalRows] = useState(0);
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchData();
    }, [page]); // Fetch data when page changes

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://localhost:8000/api/data?page=${page}&pageSize=${pageSize}`);
            setData(response.data.rows);
            setTotalRows(response.data.totalRows);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handlePageChange = (newPage) => {
        setPage(newPage);
    };

    return (
        <div>
            <table>
                {/* Render table headers */}
                <thead>
                    <tr>
                        <th>Column 1</th>
                        <th>Column 2</th>
                        {/* Add more column headers as needed */}
                    </tr>
                </thead>
                <tbody>
                    {/* Render table rows */}
                    {data.map((row, index) => (
                        <tr key={index}>
                            <td>{row.column1}</td>
                            <td>{row.column2}</td>
                            {/* Render more table cells for additional columns */}
                        </tr>
                    ))}
                </tbody>
            </table>
            {/* Pagination controls */}
            <div>
                <button onClick={() => handlePageChange(page - 1)} disabled={page === 1}>Previous</button>
                <span>Page {page}</span>
                <button onClick={() => handlePageChange(page + 1)} disabled={page * pageSize >= totalRows}>Next</button>
            </div>
            {loading && <p>Loading...</p>}
        </div>
    );
};

export default Table;
