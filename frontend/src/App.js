import React, { useState } from "react";
import SearchBar from "./SearchBar";
import ResultsList from "./ResultsList";

const App = () => {
    const [results, setResults] = useState([]);

    const handleSearch = async (query) => {
        const response = await fetch("http://localhost:5000/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query }),
        });

        const data = await response.json();
        setResults(data.results);
    };

    return (
        <div>
            <h1>AI Agent Search</h1>
            <SearchBar onSearch={handleSearch} />
            <ResultsList results={results} />
        </div>
    );
};

export default App;
