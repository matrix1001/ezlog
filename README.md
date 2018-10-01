# ezlog
Converted from `pwntools`, removed `progress`.

For those who appreciate `log` in `pwntools`, but need a single file to load it.
# usage
```python
import ezlog
log = ezlog.initLogger()
log.level = 'debug'
log.info('test msg') #[*] test msg
log.debug('test msg') #[DEBUG] test msg
```
