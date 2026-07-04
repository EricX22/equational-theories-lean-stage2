% order5v2_0898  eq1=32340 eq2=33143  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,f(Z,Y)),W)),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(f(f(Y,X),Z),Z)),Z) )).
