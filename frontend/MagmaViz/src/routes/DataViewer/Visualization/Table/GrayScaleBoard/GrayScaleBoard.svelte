<script>
    export let data;
    $: board = ("data" in data) ? data["data"] : [];
</script>

{#if board.length > 0}
    <table>
        {#each board as row}
            <tr>
                {#each row as cell}
                    <td style="background-color: rgb({cell}, {cell}, {cell})"></td>
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
