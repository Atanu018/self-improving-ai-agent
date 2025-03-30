import React from "react";

const ResultsList = ({ results }) => {
    return (
        <ul>
            {results.map((result, index) => (
                <li key={index}><a href={result} target="_blank" rel="noopener noreferrer">{result}</a></li>
            ))}
        </ul>
    );
};

export default ResultsList;
