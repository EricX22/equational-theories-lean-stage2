% order5_0169  eq1=58354 eq2=24429  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(f(X,X),Y) = f(Z,f(Z,f(X,Z))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,Y),Z),f(f(X,W),X)) )).
