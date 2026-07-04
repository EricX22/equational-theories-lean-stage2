% order5_0007  eq1=51460 eq2=3011  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(X,Z),f(X,Y)),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,f(Z,Z)),Y),X) )).
