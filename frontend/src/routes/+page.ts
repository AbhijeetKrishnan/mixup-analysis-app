import type { MixupData } from '../types/mixupData.type';


export function _updateFormRows(pageMixup: MixupData) {
    let prevRows = pageMixup.matrix.length;
    let currRows = pageMixup.rows;
    if (currRows < prevRows) {
        pageMixup.p1_strategies = pageMixup.p1_strategies.slice(0, currRows);
        pageMixup.matrix = pageMixup.matrix.slice(0, currRows);
    } else if (currRows > prevRows) {
        pageMixup.p1_strategies = [...pageMixup.p1_strategies, ...Array(currRows - prevRows).fill('')];
        pageMixup.matrix = [
            ...pageMixup.matrix,
            ...Array(currRows - prevRows).fill(Array(pageMixup.cols).fill(0))
        ];
    }
}

export function _updateFormCols(pageMixup: MixupData) {
    let prevCols = pageMixup.matrix[0].length;
		let currCols = pageMixup.cols;
		if (currCols < prevCols) {
			pageMixup.p2_strategies = pageMixup.p2_strategies.slice(0, currCols);
			pageMixup.matrix = pageMixup.matrix.map((row) => row.slice(0, currCols));
		} else if (currCols > prevCols) {
			pageMixup.p2_strategies = [...pageMixup.p2_strategies, ...Array(currCols - prevCols).fill('')];
			pageMixup.matrix = pageMixup.matrix.map((row) => [
				...row,
				...Array(currCols - prevCols).fill(0)
			]);
		}
}

export function _downloadFile(text: string, fileName: string) {
    if (typeof document !== 'undefined') {
        const blob = new Blob([text], { type: 'text/plain' });
        const blobURL = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = blobURL;
        a.download = fileName;

        a.style.display = 'none';
        document.body.appendChild(a);

        a.click();

        document.body.removeChild(a);
        URL.revokeObjectURL(blobURL);
    }
}