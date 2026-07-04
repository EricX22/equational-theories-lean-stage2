% order5_0050  eq1=13873 eq2=2630  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(f(Y,Y),Z)),Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(f(Z,W),Z)),Z) )).
