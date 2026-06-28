% hard3_0322  eq1=2998 eq2=3870  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,Y)),Z),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(X,f(Y,Y)),X) )).
