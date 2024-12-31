function FileAnalyzer() {
    const [file, setFile] = React.useState(null);
    const [progress, setProgress] = React.useState(0);
    const [error, setError] = React.useState('');
    const [analyzing, setAnalyzing] = React.useState(false);
    const [result, setResult] = React.useState(null);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setError('');
        }
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        if (!file) {
            setError('Por favor seleccione un archivo');
            return;
        }
        
        setAnalyzing(true);
        setProgress(0);
        setError('');
        
        const formData = new FormData();
        formData.append('file', file);
        
        fetch('https://ee-wx95.onrender.com/analyze', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Error en el análisis');
                });
            }
            return response.json();
        })
        .then(data => {
            setResult(data);
            setAnalyzing(false);
            setProgress(100);
        })
        .catch(error => {
            console.error('Error details:', error);
            setError('Error al procesar el archivo: ' + (error.message || 'Error desconocido'));
            setAnalyzing(false);
            setProgress(0);
        });
    };

    return (
        <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md mx-auto">
                <div className="text-center">
                    <h2 className="text-3xl font-bold text-gray-900 mb-8">
                        Analizador de Archivos
                    </h2>
                </div>

                <div className="bg-white p-8 rounded-lg shadow-md">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-4">
                            <label className="block text-sm font-medium text-gray-700">
                                Seleccionar Archivo
                            </label>
                            
                            <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-blue-500 transition-colors">
                                <div className="space-y-1 text-center">
                                    <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                                        <path d="M24 8v32M8 24h32" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                                    </svg>
                                    <div className="flex text-sm text-gray-600">
                                        <label className="relative cursor-pointer rounded-md font-medium text-blue-600 hover:text-blue-500">
                                            <span>Subir un archivo</span>
                                            <input
                                                type="file"
                                                className="sr-only"
                                                onChange={handleFileChange}
                                                accept=".docx"
                                            />
                                        </label>
                                    </div>
                                    <p className="text-xs text-gray-500">
                                        {file ? file.name : 'DOCX hasta 10MB'}
                                    </p>
                                </div>
                            </div>
                        </div>

                        {error && (
                            <div className="bg-red-50 border-l-4 border-red-400 p-4">
                                <p className="text-red-700">{error}</p>
                            </div>
                        )}

                        {analyzing && (
                            <div className="space-y-2">
                                <div className="h-2 bg-gray-200 rounded-full">
                                    <div
                                        className="h-2 bg-blue-600 rounded-full transition-all duration-500"
                                        style={{ width: `${progress}%` }}
                                    />
                                </div>
                                <p className="text-sm text-gray-600 text-center">
                                    Analizando... {progress}%
                                </p>
                            </div>
                        )}

                        {result && (
                            <div className="mt-4 space-y-4">
                                <div className="bg-gray-50 p-4 rounded-md">
                                    <h3 className="text-lg font-medium text-gray-900 mb-2">Análisis:</h3>
                                    <div className="prose max-w-none">
                                        {result.analysis}
                                    </div>
                                </div>
                            </div>
                        )}

                        <button
                            type="submit"
                            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                            disabled={analyzing}
                        >
                            {analyzing ? 'Procesando...' : 'Analizar Archivo'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

ReactDOM.render(<FileAnalyzer />, document.getElementById('root'));
