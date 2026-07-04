% order5_0233  eq1=58748 eq2=10079  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(X,f(W,f(X,X))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(Y,Y),f(f(Z,W),Y))) )).
