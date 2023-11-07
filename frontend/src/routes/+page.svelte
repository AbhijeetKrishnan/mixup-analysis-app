<script lang="ts">
	let title = 'Untitled strategic game';
	let comment = '';
	let player_1 = '1';
	let player_2 = '2';
	let p1_strategies = ['', ''];
	let p2_strategies = ['', ''];
	let rows = 2;
	let cols = 2;
	let data = [
		[1, 2],
		[3, 4]
	];
	let p1_probs = [null, null];
	let p2_probs = [null, null];
	let payoff: number = 0.0;
</script>

<h1>Mixup Analysis Frontend</h1>

<div>
	<label for="title">Title</label>
	<input type="text" id="title" name="title" bind:value={title} />

	<label for="comment">Comment</label>
	<input type="text" id="comment" name="comment" bind:value={comment} />

	<label for="player_1">Player 1</label>
	<input type="text" id="player_1" name="player_1" bind:value={player_1} />

	<label for="player_2">Player 2</label>
	<input type="text" id="player_2" name="player_2" bind:value={player_2} />

	<label for="rows">Rows</label>
	<input type="number" id="rows" min="1" max="10" bind:value={rows} />

	<label for="cols">Columns</label>
	<input type="number" id="cols" name="cols" min="1" max="10" bind:value={cols} />

	{#each Array(rows) as _, i}
		<p>{p1_strategies[i]}</p>
	{/each}

	{#each Array(cols) as _, i}
		<p>{p2_strategies[i]}</p>
	{/each}

	{#each Array(rows) as _, i}
		<p>{p1_probs[i]}</p>
	{/each}

	{#each Array(cols) as _, i}
		<p>{p2_probs[i]}</p>
	{/each}

	<p>Payoff: {payoff}</p>

	<table>
		{#each Array(rows) as _, i}
			<tr>
				{#each Array(cols) as _, j}
					<td><input type="number" id="{i}-{j}" name="{i}-{j}" bind:value={data[i][j]} /></td>
				{/each}
			</tr>
		{/each}
	</table>
</div>
