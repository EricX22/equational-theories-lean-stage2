% hard3_0140  eq1=1072 eq2=1251  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(f(X,f(X,X)),X)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(f(Y,Y),Y),X)) )).
