<script lang="ts">
	import type { MixupData } from '../types/mixupData.type';
	import type { ActionData, PageData } from './$types';

	export let data: PageData;
	export let form: ActionData;
	console.log('Page data', data);
	console.log('Action data', form);

	let formData: MixupData;
	let fileText: string;
	if (form !== null && typeof form !== 'string' && Object.keys(form).length !== 0) {
		formData = form as MixupData;
	} else if (typeof form === 'string') {
		console.log('Action string', form);
		fileText = form;
	} else {
		formData = {
			title: 'Untitled strategic game',
			comment: '',
			player_1: '1',
			player_2: '2',
			rows: 2,
			cols: 2,
			p1_strategies: ['s1-1', 's1-2'],
			p2_strategies: ['s2-1', 's2-2'],
			matrix: [
				[1, -1],
				[-3, 3]
			],
			p1_probs: null,
			p2_probs: null,
			payoff: null
		};
	}

	$: {
		let prevRows = formData.matrix.length;
		let currRows = formData.rows;
		if (currRows < prevRows) {
			formData.p1_strategies = formData.p1_strategies.slice(0, currRows);
			formData.matrix = formData.matrix.slice(0, currRows);
		} else if (currRows > prevRows) {
			formData.p1_strategies = [...formData.p1_strategies, ...Array(currRows - prevRows).fill('')];
			formData.matrix = [
				...formData.matrix,
				...Array(currRows - prevRows).fill(Array(formData.cols).fill(0))
			];
		}
	}

	$: {
		let prevCols = formData.matrix[0].length;
		let currCols = formData.cols;
		if (currCols < prevCols) {
			formData.p2_strategies = formData.p2_strategies.slice(0, currCols);
			formData.matrix = formData.matrix.map((row) => row.slice(0, currCols));
		} else if (currCols > prevCols) {
			formData.p2_strategies = [...formData.p2_strategies, ...Array(currCols - prevCols).fill('')];
			formData.matrix = formData.matrix.map((row) => [
				...row,
				...Array(currCols - prevCols).fill(0)
			]);
		}
	}
</script>

<h1 class="text-2xl">Mixup Analysis Frontend</h1>

<form method="POST">
	<label for="title">Title</label>
	<input type="text" name="title" bind:value={formData.title} />

	<label for="comment">Comment</label>
	<input type="text" name="comment" bind:value={formData.comment} />

	<label for="player_1">Player 1</label>
	<input type="text" name="player_1" bind:value={formData.player_1} />

	<label for="player_2">Player 2</label>
	<input type="text" name="player_2" bind:value={formData.player_2} />

	<label for="rows">Rows</label>
	<input type="number" name="rows" min="1" max="10" required bind:value={formData.rows} />

	<label for="cols">Columns</label>
	<input type="number" name="cols" min="1" max="10" required bind:value={formData.cols} />

	{#each Array(formData.rows) as _, i}
		<input type="text" name="s1-{i}" bind:value={formData.p1_strategies[i]} />
	{/each}

	{#each Array(formData.cols) as _, j}
		<input type="text" name="s2-{j}" bind:value={formData.p2_strategies[j]} />
	{/each}

	<table class="grid-cols-{formData.cols}">
		{#each Array(formData.rows) as _, i}
			<tr>
				{#each Array(formData.cols) as _, j}
					{#if i < formData.rows && j < formData.cols}
						<td><input type="number" name="cell-{i}-{j}" bind:value={formData.matrix[i][j]} /></td>
					{/if}
				{/each}
			</tr>
		{/each}
	</table>

	<button name="analyze" type="submit" formaction="?/analyze">Analyze</button>

	<button name="save" type="submit" formaction="?/download">Save</button>
	<!-- TODO: enable downloading of file -->

	<button name="load" type="submit" formaction="?/upload">Load</button>
</form>

{#if formData.p1_probs !== null && formData.p2_probs !== null && formData.payoff !== null}
	{#each Array(formData.rows) as _, i}
		<p>Strategy {i} prob: {formData.p1_probs[i][0] / formData.p1_probs[i][1]}</p>
	{/each}

	{#each Array(formData.cols) as _, i}
		<p>Strategy {i} prob: {formData.p2_probs[i][0] / formData.p2_probs[i][1]}</p>
	{/each}

	<p>Payoff: {formData.payoff[0] / formData.payoff[1]}</p>
{/if}
