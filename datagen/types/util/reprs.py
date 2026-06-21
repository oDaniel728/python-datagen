from typing import Any, Literal


type double = float
type boolean = int | bool | Literal['0', '1']
type short = int
type byte = int
type compound[K = str, V = Any] = dict[K, V]
type array[T = Any] = list[T]
type tuple2[T] = tuple[T, T] | list[T] | set[T]
type tuple3[T] = tuple[T, T, T] | list[T] | set[T]