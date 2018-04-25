1. dpkg 

> 29[down vote]()accepted
>
> First of all you should check if this package is correctly installed in your system and being listed by `dpkg` tool:
>
> `dpkg -l | grep urserver`
>
> It should have an option `ii` in the first column of the output - that means 'installed ok installed'.
>
> If you'd like to remove the package itself (without the configuration files), you'll have to run:
>
> `dpkg -r urserver`
>
> If you'd like to delete (purge) the package completely (with configuration files), you'll have to run:
>
> `dpkg -P urserver`
>
> You may check if the package has been removed successfully - simply run again:
>
> `dpkg -l | grep urserver`
>
> If the package has been removed without configuration files, you'll see the `rc` status near the package name, otherwise, if you have purged the package completely, the output will be empty.