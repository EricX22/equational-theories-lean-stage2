% hard3_0315  eq1=2927 eq2=765  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,f(X,Z)),Z),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Z,f(f(Y,Z),X))) )).
