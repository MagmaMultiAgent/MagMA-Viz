<script>
    export let board;
</script>

{#if board !== undefined && board.length > 0}
    <table id="container">
        {#each rgbBoard as row}
            <tr>
                {#each row as cell}
                    <td style="background-color: rgb({cell}, {cell}, {cell})"></td>
                {/each}
            </tr>
        {/each}
    </table>
{/if}