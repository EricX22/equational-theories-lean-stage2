% hard3_0303  eq1=2856 eq2=616  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(X,f(X,Y)),Y),Y) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(X,f(X,f(f(X,Y),X))) )).
