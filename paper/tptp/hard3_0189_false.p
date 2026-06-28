% hard3_0189  eq1=1681 eq2=2203  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(Y,X),f(f(X,X),X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,Z),Z),f(Z,X)) )).
