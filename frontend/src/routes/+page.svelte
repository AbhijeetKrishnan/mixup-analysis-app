<script lang="ts">
	import type { MixupData } from '../types/mixupData.type';
	import type { ActionData } from './$types';

	export let form: ActionData;
	let formData: MixupData;

	if (form !== null && Object.keys(form).length !== 0) {
		formData = form['mixup'] as MixupData;
		if ('nfg' in form) {
			downloadFile(form['nfg'], 'game.nfg');
		}
	} else {
		formData = {
			title: '',
			comment: '',
			player_1: '',
			player_2: '',
			rows: 2,
			cols: 2,
			p1_strategies: ['', ''],
			p2_strategies: ['', ''],
			matrix: [
				[0, 0],
				[0, 0]
			],
			p1_probs: null,
			p2_probs: null,
			payoff: null
		};
	}

	function downloadFile(text: string, fileName: string) {
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

<div
	class="align-items-center md:px-15 container flex min-h-screen min-w-full flex-col justify-center justify-items-center from-gray-900 to-gray-800 px-5 dark:bg-gradient-to-r sm:px-10 lg:px-20"
>
	<h1
		class="p-4 text-center text-3xl font-extrabold text-gray-900 dark:text-white sm:text-4xl md:text-5xl lg:text-6xl"
	>
		Mixup Analysis Frontend
	</h1>

	<form method="POST">
		<div class="mx-auto max-w-max">
			<fieldset
				class="align-items-center my-10 grid grid-cols-1 justify-items-center divide-y-0 divide-gray-300 rounded-lg dark:divide-gray-600 dark:bg-gray-700"
			>
				<div
					class="w-full rounded-t-lg border border-gray-300 px-2 py-1.5 focus-within:border focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 dark:border-gray-600"
				>
					<label
						for="title"
						class="leading-1 block w-full text-xs font-bold text-gray-900 dark:text-white"
						>Title</label
					>
					<input
						type="text"
						class="block w-full bg-inherit text-base text-gray-900 focus:outline-none dark:text-white dark:placeholder-gray-400"
						name="title"
						placeholder="Untitled strategic game"
						tabindex="0"
						bind:value={formData.title}
					/>
				</div>

				<div
					class="w-full rounded-b-lg border border-gray-300 px-2 py-1.5 focus-within:border focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500 dark:border-gray-600"
				>
					<label
						for="comment"
						class="leading-1 block w-full bg-inherit text-xs font-bold text-gray-900 dark:text-white"
						>Comment</label
					>
					<input
						type="text"
						name="comment"
						placeholder="A comment about the mixup here"
						tabindex="0"
						class="block w-full bg-inherit text-base text-gray-900 focus:outline-none dark:text-white dark:placeholder-gray-400"
						bind:value={formData.comment}
					/>
				</div>
			</fieldset>

			<fieldset
				class="my-10 grid grid-cols-2 divide-x-0 divide-gray-300 rounded-lg dark:divide-gray-600 dark:bg-gray-700"
			>
				<div
					class="w-full rounded-l-lg border px-2 py-1.5 focus-within:border focus-within:border-rose-500 focus-within:ring-1 focus-within:ring-rose-500 dark:border-gray-600"
				>
					<label
						for="player_1"
						class="leading-1 block w-full text-xs font-bold text-gray-900 dark:text-white"
						>Player 1</label
					>
					<input
						type="text"
						name="player_1"
						class="block w-full bg-inherit text-base text-gray-900 focus:outline-none dark:text-white dark:placeholder-gray-400"
						placeholder="Attacker"
						tabindex="0"
						bind:value={formData.player_1}
					/>
				</div>
				<div
					class="w-full rounded-r-lg border px-2 py-1.5 focus-within:border focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500 dark:border-gray-600"
				>
					<label
						for="player_2"
						class="leading-1 block w-full text-xs font-bold text-gray-900 dark:text-white"
						>Player 2</label
					>
					<input
						type="text"
						name="player_2"
						placeholder="Defender"
						tabindex="0"
						class="block w-full bg-inherit text-base text-gray-900 focus:outline-none dark:text-white dark:placeholder-gray-400"
						bind:value={formData.player_2}
					/>
				</div>
			</fieldset>

			<fieldset
				class="my-10 grid grid-cols-2 divide-x-0 divide-gray-300 rounded-lg dark:divide-gray-600 dark:bg-gray-700"
			>
				<div
					class="w-full rounded-l-lg border px-2 py-1.5 focus-within:border focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 dark:border-gray-600"
				>
					<label
						for="rows"
						class="leading-1 block w-full text-xs font-bold text-gray-900 dark:text-white"
						>Attacker Strategies</label
					>
					<input
						type="number"
						class="block w-full bg-inherit pr-1 text-base text-gray-900 focus:outline-none dark:text-white"
						name="rows"
						min="1"
						required
						tabindex="0"
						bind:value={formData.rows}
					/>
				</div>
				<div
					class="w-full rounded-r-lg border px-2 py-1.5 focus-within:border focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500 dark:border-gray-600"
				>
					<label
						for="cols"
						class="leading-1 block w-full text-xs font-bold text-gray-900 dark:text-white"
						>Defender Strategies</label
					>
					<input
						type="number"
						class="block w-full bg-inherit pr-1 text-base text-gray-900 focus:outline-none dark:text-white"
						name="cols"
						min="1"
						required
						tabindex="0"
						bind:value={formData.cols}
					/>
				</div>
			</fieldset>
		</div>

		<!-- TODO: implement reset button here to reset grid to 2x2 -->

		<div>
			<table class="my-10 w-full table-auto border-collapse">
				<tr class="flex w-full">
					<td class="block w-full bg-transparent px-2 py-1.5"></td>
					{#each Array(formData.cols) as _, j}
						<td
							class="block w-full border border-gray-300 px-2 py-1.5 dark:border-gray-600 dark:bg-gray-700"
						>
							<input
								type="text"
								class="block w-full bg-inherit text-sm text-gray-900 focus:outline-none dark:text-white dark:placeholder-gray-400"
								name="s2-{j}"
								tabindex="1"
								placeholder="Defender strategy {j}"
								bind:value={formData.p2_strategies[j]}
							/>
						</td>
					{/each}
				</tr>

				{#each Array(formData.rows) as _, i}
					<tr class="flex w-full">
						<td
							class="block w-full border border-gray-300 px-2 py-1.5 dark:border-gray-600 dark:bg-gray-700"
						>
							<input
								type="text"
								name="s1-{i}"
								placeholder="Attacker strategy {i}"
								tabindex="0"
								class="block w-full bg-inherit text-sm text-gray-900 focus:outline-none dark:text-white dark:placeholder-gray-400"
								bind:value={formData.p1_strategies[i]}
							/>
						</td>
						{#each Array(formData.cols) as _, j}
							<td
								class="block w-full border border-gray-300 px-2 py-1.5 dark:border-gray-600 dark:bg-gray-700"
								><input
									type="number"
									class="block w-full bg-inherit pr-1 text-base text-gray-900 focus:border-blue-500 focus:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
									name="cell-{i}-{j}"
									tabindex="2"
									bind:value={formData.matrix[i][j]}
								/></td
							>
						{/each}
					</tr>
				{/each}
			</table>

			<div class="flex flex-row justify-center pb-5 align-middle">
				<button
					name="analyze"
					class="mx-2 rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700"
					type="submit"
					tabindex="3"
					formaction="?/analyze">Analyze</button
				>

				<button
					name="save"
					type="submit"
					class="mx-2 inline-flex items-center rounded bg-gray-300 px-4 py-2 font-bold text-gray-800 hover:bg-gray-400"
					formaction="?/download"
					tabindex="3"
					><svg
						class="mr-2 h-4 w-4 fill-current"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 20 20"><path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z" /></svg
					>
					<span>Save</span></button
				>

				<!-- TODO: implement this flow better; it should be 1. click on 'Load' button, 2. open file picker, 3. populate with values -->
				<!-- <label for="upload-file">Load</label>
			<input
				name="upload-file"
				type="file"
				accept="text/plain"
				class="mx-2 w-full text-white
		file:mr-4 file:rounded file:border-0
		file:bg-blue-500 file:px-4
		file:py-2
		file:font-semibold file:text-white
		hover:file:bg-blue-700"
				formaction="?/upload"
				tabindex=3
			/>
			<button
				name="save"
				type="submit"
				formaction="?/upload"
				tabindex=3	
				class="mx-2 inline-flex items-center rounded bg-gray-300 px-4 py-2 font-bold text-gray-800 hover:bg-gray-400"
				><svg
					class="mr-2 h-4 w-4 fill-current"
					aria-hidden="true"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 20 19"
				>
					<path
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M15 15h.01M4 12H2a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1h-3m-5.5 0V1.07M5.5 5l4-4 4 4"
					/>
				</svg><span>Load</span></button
			> -->
			</div>
		</div>
	</form>

	<!-- TODO: Analysis data doesn't persist if Save is called -->
	<!-- TODO: Separate out analysis and form data maybe? -->
	<!-- TODO: check analysis results; they don't seem to match up with wavu -->
	<!-- TODO: style analysis content -->
	{#if formData.p1_probs !== null && formData.p2_probs !== null && formData.payoff !== null}
		{#each Array(formData.p1_probs.length) as _, i}
			<p>Strategy {i} prob: {formData.p1_probs[i][0] / formData.p1_probs[i][1]}</p>
		{/each}

		{#each Array(formData.p2_probs.length) as _, i}
			<p>Strategy {i} prob: {formData.p2_probs[i][0] / formData.p2_probs[i][1]}</p>
		{/each}

		<p>Payoff: {formData.payoff[0] / formData.payoff[1]}</p>
	{/if}
</div>
