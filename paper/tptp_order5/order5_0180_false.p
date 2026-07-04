% order5_0180  eq1=22505 eq2=46912  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(Y,f(X,Y)),f(f(Z,Z),Z)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,X) != f(f(Y,Y),f(f(Z,W),X)) )).
