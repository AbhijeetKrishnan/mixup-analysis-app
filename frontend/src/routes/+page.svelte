<script lang="ts">
	import type { MixupData } from '../types/mixupData.type';

	export let formData: MixupData = {
		title: 'Untitled strategic game',
		comment: '',
		player_1: '1',
		player_2: '2',
		rows: 2,
		cols: 2,
		p1_strategies: ['s1-1', 's1-2'],
		p2_strategies: ['s2-1', 's2-2'],
		data: [
			[1, -1],
			[-3, 3]
		],
		p1_probs: null,
		p2_probs: null,
		payoff: null
	};
	export let onSubmit = () => {};

	let title = formData.title ?? 'Untitled strategic game';
	let comment = formData.comment ?? '';
	let player_1 = formData.player_1 ?? '1';
	let player_2 = formData.player_2 ?? '2';
	let rows = formData.rows ?? 2;
	let cols = formData.cols ?? 2;
	let p1_strategies = formData.p1_strategies ?? ['s1-1', 's1-2'];
	let p2_strategies = formData.p2_strategies ?? ['s2-1', 's2-2'];
	let data = formData.data ?? [
		[1, -1],
		[-3, 3]
	];
	let p1_probs = formData.p1_probs ?? null;
	let p2_probs = formData.p2_probs ?? null;
	let payoff = formData.payoff ?? null;

	$: {
		let prevRows = data.length;
		let currRows = rows;
		if (currRows < prevRows) {
			p1_strategies = p1_strategies.slice(0, currRows);
			data = data.slice(0, currRows);
		} else if (currRows > prevRows) {
			p1_strategies = [...p1_strategies, ...Array(currRows - prevRows).fill('')];
			data = [...data, ...Array(currRows - prevRows).fill(Array(cols).fill(0))];
		}
		// console.log(prevRows, currRows);
		// console.log(data);
	}

	$: {
		let prevCols = data[0].length;
		let currCols = cols;
		if (currCols < prevCols) {
			p2_strategies = p2_strategies.slice(0, currCols);
			data = data.map((row) => row.slice(0, currCols));
		} else if (currCols > prevCols) {
			p2_strategies = [...p2_strategies, ...Array(currCols - prevCols).fill('')];
			data = data.map((row) => [...row, ...Array(currCols - prevCols).fill(0)]);
		}
	}
</script>

<h1 class="text-2xl">Mixup Analysis Frontend</h1>

<form method="POST" on:submit|preventDefault={onSubmit}>
	<label for="title">Title</label>
	<input type="text" id="title" name="title" bind:value={title} />

	<label for="comment">Comment</label>
	<input type="text" id="comment" name="comment" bind:value={comment} />

	<label for="player_1">Player 1</label>
	<input type="text" id="player_1" name="player_1" bind:value={player_1} />

	<label for="player_2">Player 2</label>
	<input type="text" id="player_2" name="player_2" bind:value={player_2} />

	<label for="rows">Rows</label>
	<input type="number" id="rows" min="1" max="10" required bind:value={rows} />

	<label for="cols">Columns</label>
	<input type="number" id="cols" name="cols" min="1" max="10" required bind:value={cols} />

	{#each Array(rows) as _, i}
		<p>{p1_strategies[i]}</p>
	{/each}

	{#each Array(cols) as _, j}
		<p>{p2_strategies[j]}</p>
	{/each}

	<table class="grid-cols-{cols}">
		{#each Array(rows) as _, i}
			<tr>
				{#each Array(cols) as _, j}
					{#if i < rows && j < cols}
						<td
							><input
								type="number"
								id="cell-{i}-{j}"
								name="cell-{i}-{j}"
								bind:value={data[i][j]}
							/></td
						>
					{/if}
				{/each}
			</tr>
		{/each}
	</table>

	{#if p1_probs != null && p2_probs != null && payoff != null}
		{#each Array(rows) as _, i}
			<p>{p1_probs[i]}</p>
		{/each}

		{#each Array(cols) as _, i}
			<p>{p2_probs[i]}</p>
		{/each}

		<p>Payoff: {payoff}</p>
	{/if}

	<button name="analyze" type="submit" formaction="/analyze">Analyze</button>

	<button name="save" type="submit" formaction="/download">Save</button>

	<button name="load" type="submit" formaction="/upload">Load</button>
</form>
