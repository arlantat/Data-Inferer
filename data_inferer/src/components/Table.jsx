// Table.js
import React, {useState} from 'react';

const Table = ({ data, itemsPerPage }) => {
    const [currentPage, setCurrentPage] = useState(1);
    const [currentDf, setCurrentDf] = useState('df');
    const [currentDtype, setCurrentDtype] = useState('df_dtype');

    if (!data || data['error']) return null;

    const totalPages = Math.ceil(data[currentDf][Object.keys(data[currentDf])[0]].length / itemsPerPage);

    const handleNextPage = () => {
        if (currentPage < totalPages) {
            setCurrentPage(currentPage + 1);
        }
    };

    const handlePrevPage = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    const handleInputPage = (e) => {
        let page = parseInt(e.target.value);
        if (!isNaN(page) && page >= 1 && page <= totalPages) {
            setCurrentPage(page);
        }
    };

    const changeDfState = () => {
        if (currentDf === 'df') {
            setCurrentDf('converted_df');
            setCurrentDtype('converted_df_dtype');
        } else {
            setCurrentDf('df');
            setCurrentDtype('df_dtype');
        }
    }

    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, data[currentDf][Object.keys(data[currentDf])[0]].length);

    return (
        <div>
            <div className={"table-head"}>
                <button onClick={handlePrevPage} disabled={currentPage === 1}>Previous Page</button>
                <span>Page {currentPage} of {totalPages}</span>
                <input type="number" value={currentPage} onChange={handleInputPage}/>
                <button onClick={handleNextPage} disabled={currentPage === totalPages}>Next Page</button>
                <button onClick={changeDfState}>Switch Original/Modified Data</button>
            </div>
            <div className="table-responsive">
                <table className="table table-bordered">
                    <thead>
                        <tr>
                            {Object.keys(data[currentDf]).map((key) => (
                                <th key={key}>{key}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data[currentDf][Object.keys(data[currentDf])[0]].slice(startIndex, endIndex).map((_, rowIndex) => (
                            <tr key={rowIndex}>
                                {Object.keys(data[currentDf]).map((columnName, colIndex) => (
                                    <td key={`${rowIndex}-${colIndex}`}>{data[currentDf][columnName][startIndex + rowIndex]}</td>
                                ))}
                            </tr>
                        ))}
                        <tr>
                            {data[currentDtype].map((value, colIndex) => (
                                <td key={`dtype-${colIndex}`} style={{fontWeight: 'bold'}}>{value}</td>
                            ))}
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Table;
