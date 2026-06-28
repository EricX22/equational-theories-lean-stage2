% hard3_0199  eq1=1844 eq2=2448  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(X,Y)),f(Z,Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(f(X,Y),X)),Z) )).
