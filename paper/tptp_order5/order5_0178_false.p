% order5_0178  eq1=30393 eq2=12347  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(X,f(f(Y,Z),Y))),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(f(f(Z,Y),W),f(X,W))) )).
