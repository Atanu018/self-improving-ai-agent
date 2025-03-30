const handleSearch = async (query) => {
    try {
        const response = await fetch("http://localhost:5000/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Ensure results is always an array
        setResults(Array.isArray(data.results) ? data.results : []);

    } catch (error) {
        console.error("Error fetching search results:", error);
        setResults([]); // Set empty array on error
    }
};
