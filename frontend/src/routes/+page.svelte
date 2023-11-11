<script lang="ts">
	import type { MixupData, AnalysisData } from '../types/mixupData.type';
	import { mixupInitVal } from '../types/mixupData.type';
	import type { ActionData } from './$types';
	import { _updateFormRows, _downloadFile, _updateFormCols } from './+page';

	export let form: ActionData;

	let currMixup: MixupData = mixupInitVal;
	let currAnalysis: AnalysisData;

	if (form !== null && Object.keys(form).length !== 0) {
		switch (form['type']) {
			case 'analyze': {
				currMixup = form['orig'] as MixupData;
				currAnalysis = form['result'];
				break;
			}
			case 'download': {
				currMixup = form['orig'] as MixupData;
				_downloadFile(form['result'], 'game.nfg');
				break;
			}
			case 'upload': {
				currMixup = form['result'];
				break;
			}
		}
	}

	$: {
		_updateFormRows(currMixup);
	}

	$: {
		_updateFormCols(currMixup);
	}

	function resetMatrix() {
		currMixup.rows = 2;
		currMixup.cols = 2;
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
						bind:value={currMixup.title}
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
						bind:value={currMixup.comment}
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
						bind:value={currMixup.player_1}
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
						bind:value={currMixup.player_2}
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
						bind:value={currMixup.rows}
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
						bind:value={currMixup.cols}
					/>
				</div>
			</fieldset>
		</div>

		<div>
			<table class="my-10 w-full table-auto border-collapse">
				<tr class="flex w-full">
					<td class="block w-full bg-transparent px-2 py-1.5"
						><button
							type="button"
							class="mb-2 me-2 rounded-full bg-blue-500 px-2 py-0 text-center text-xs font-light text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
							on:click={resetMatrix}>Reset</button
						></td
					>
					{#each Array(currMixup.cols) as _, j}
						<td
							class="block w-full border border-gray-300 px-2 py-1.5 dark:border-gray-600 dark:bg-gray-700"
						>
							<input
								type="text"
								class="block w-full bg-inherit text-sm text-gray-900 focus:outline-none dark:text-white dark:placeholder-gray-400"
								name="s2-{j}"
								tabindex="1"
								placeholder="Defender strategy {j}"
								bind:value={currMixup.p2_strategies[j]}
							/>
						</td>
					{/each}
				</tr>

				{#each Array(currMixup.rows) as _, i}
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
								bind:value={currMixup.p1_strategies[i]}
							/>
						</td>
						{#each Array(currMixup.cols) as _, j}
							<td
								class="block w-full border border-gray-300 px-2 py-1.5 dark:border-gray-600 dark:bg-gray-700"
								><input
									type="number"
									class="block w-full bg-inherit pr-1 text-base text-gray-900 focus:border-blue-500 focus:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
									name="cell-{i}-{j}"
									tabindex="2"
									bind:value={currMixup.matrix[i][j]}
								/></td
							>
						{/each}
					</tr>
				{/each}
			</table>

			<!-- Have buttons submit to custom script in +page.ts -->
			<div class="flex flex-row justify-center justify-items-center pb-5">
				<button
					name="analyze"
					class="mx-2 rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700"
					type="submit"
					tabindex="3"
					formaction="?/analyze">Analyze</button
				>

				<button
					name="download"
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
			</div>
		</div>
	</form>
	<form method="POST" enctype="multipart/form-data" class="mx-auto">
		<!-- TODO: implement this flow better; it should be 1. click on 'Load' button, 2. open file picker, 3. populate with values -->
		<input
			name="upload_file"
			type="file"
			accept=".nfg,.gbt"
			class="-mr-15 text-white file:mx-2 file:mr-4 file:rounded file:border-0 file:bg-blue-500 file:px-4 file:py-2 file:font-bold file:text-white hover:file:bg-blue-700"
			formaction="?/upload"
			tabindex="3"
		/>
		<button
			name="upload"
			type="submit"
			formaction="?/upload"
			tabindex="3"
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
		>
	</form>

	<!-- TODO: Analysis data doesn't persist if Save is called -->
	<!-- TODO: page reloads to top when analysis is pressed. Try to get it to focus on the bottom -->
	{#if currAnalysis !== undefined}
		<div class="mx-auto mb-5 mt-5 max-w-max text-white">
			<div class="font-base text-center text-2xl font-semibold">Payoffs</div>
			<div class="flex w-full flex-row justify-items-center gap-x-20">
				<div
					class="align-items-center my-10 flex w-full flex-col rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700"
				>
					<div
						class="w-full border-b border-gray-300 text-center font-semibold dark:border-gray-600"
					>
						{currMixup.player_1}
					</div>
					{#each Array(currAnalysis.p1_probs.length) as _, i}
						<div class="flex w-full flex-row">
							<div class="h-fit w-1/2 px-3 text-center">{currMixup.p1_strategies[i]}</div>
							<div class="w-1/2 px-3 text-right">
								{currAnalysis.p1_probs[i][0] / currAnalysis.p1_probs[i][1]}
							</div>
						</div>
					{/each}
				</div>

				<div
					class="align-items-center my-10 flex flex-col rounded-lg border border-gray-300 text-white dark:border-gray-600 dark:bg-gray-700"
				>
					<div
						class="w-full border-b border-gray-300 text-center font-semibold dark:border-gray-600"
					>
						{currMixup.player_2}
					</div>
					{#each Array(currAnalysis.p2_probs.length) as _, i}
						<div class="flex w-full flex-row">
							<div class="h-fit w-1/2 px-3 text-center">{currMixup.p2_strategies[i]}</div>
							<div class="w-1/2 px-3 text-right">
								{currAnalysis.p2_probs[i][0] / currAnalysis.p2_probs[i][1]}
							</div>
						</div>
					{/each}
				</div>
			</div>

			<div class="text-center">
				<div>Payoff</div>
				<div>
					{currAnalysis.payoff[0] / currAnalysis.payoff[1]}
				</div>
			</div>
		</div>
	{/if}
</div>
