<script>
    export let board;
</script>

{#if board !== undefined && board.length > 0}
    <table id="container">
        {#each rgbBoard as row}
            <tr>
                {#each row as cell}
                    {#if cell.length === 3}
                        <td style="background-color: rgb({cell[0]}, {cell[1]}, {cell[2]})"></td>
                    {/if}
                {/each}
            </tr>
        {/each}
    </table>
{/if}