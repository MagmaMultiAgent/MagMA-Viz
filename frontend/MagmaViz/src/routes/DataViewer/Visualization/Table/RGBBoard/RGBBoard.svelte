<script>
    export let data;
    $: board = ("data" in data) ? data["data"] : [];
</script>

{#if board.length > 0}
    <table>
        {#each board as row}
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

<style>
    table {
        width: 100%;
        border-collapse: collapse;
    }

    td {
        width: 0;
        padding: 0;
    }

    td:before {
        content: "";
        display: block;
        padding-top: 100%;
    }
</style>
