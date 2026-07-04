% order5_0160  eq1=42511 eq2=9725  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(Y,f(Y,f(f(Y,Z),X))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(Z,Y),f(W,f(Z,Z)))) )).
