% order5_0110  eq1=39516 eq2=30850  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(f(Y,Z),f(Y,Z)),X),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(Z,f(f(Z,W),Z))),Z) )).
