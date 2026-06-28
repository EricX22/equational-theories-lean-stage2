% hard3_0374  eq1=3745 eq2=377  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(X,Z),f(W,Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(X,Y),X) )).
