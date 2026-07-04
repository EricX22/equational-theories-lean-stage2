% order5_0106  eq1=52321 eq2=12315  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(f(X,f(Y,Z)),Z),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(f(f(Z,Y),Y),f(Y,Y))) )).
